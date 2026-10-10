import * as faceapi from '@vladmandic/face-api'

/* -------------------------------------------------------------------------- */
/*  Erros                                                                     */
/* -------------------------------------------------------------------------- */

export type FaceErrorCode = 'INVALID_INPUT' | 'NO_FACE' | 'MODELS_FAILED'

export class FaceAnalysisError extends Error {
  code: FaceErrorCode

  constructor(code: FaceErrorCode, message: string) {
    super(message)
    this.name = 'FaceAnalysisError'
    this.code = code
  }
}

/* -------------------------------------------------------------------------- */
/*  Carregamento de modelos                                                   */
/* -------------------------------------------------------------------------- */

let modelsReady = false
let modelsPromise: Promise<void> | null = null

/**
 * Carrega apenas o necessário para criação de personagens:
 * detector + 68 landmarks. O faceRecognitionNet (descritor 128D) foi removido
 * porque só serve para comparar identidades, não para medir proporções, e
 * pesa ~6 MB a mais.
 */
export function loadModels(modelsPath = '/models'): Promise<void> {
  if (modelsReady) return Promise.resolve()

  if (!modelsPromise) {
    modelsPromise = Promise.all([
      faceapi.nets.tinyFaceDetector.loadFromUri(modelsPath),
      faceapi.nets.faceLandmark68Net.loadFromUri(modelsPath),
    ])
      .then(() => {
        modelsReady = true
      })
      .catch((error) => {
        modelsPromise = null // permite tentar de novo
        console.error('Erro ao carregar os modelos faciais:', error)
        throw new FaceAnalysisError(
          'MODELS_FAILED',
          'Não foi possível carregar os modelos de análise facial.',
        )
      })
  }

  return modelsPromise
}

/* -------------------------------------------------------------------------- */
/*  Tipos públicos                                                            */
/* -------------------------------------------------------------------------- */

/** Aceita upload (File/Blob), <img>, <video> (câmera ao vivo), <canvas> e ImageBitmap. */
export type FaceInput =
  | Blob
  | HTMLImageElement
  | HTMLVideoElement
  | HTMLCanvasElement
  | ImageBitmap

export interface Point {
  x: number
  y: number
}

export type FaceShape = 'oval' | 'round' | 'square' | 'heart' | 'oblong'

export type TraitKey =
  | 'faceLength' // rosto curto -> alongado
  | 'jawWidth' // mandíbula estreita -> larga
  | 'chinPointiness' // queixo arredondado -> pontudo
  | 'eyeSpacing' // olhos próximos -> afastados
  | 'eyeSize' // olhos pequenos -> grandes
  | 'eyeOpenness' // olhos estreitos -> abertos
  | 'noseWidth' // nariz estreito -> largo
  | 'noseLength' // nariz curto -> longo
  | 'mouthWidth' // boca pequena -> larga
  | 'lipFullness' // lábios finos -> grossos

export type FaceWarning =
  | 'MULTIPLE_FACES'
  | 'FACE_TOO_SMALL'
  | 'FACE_CUT_OFF'
  | 'LOW_CONFIDENCE'
  | 'HEAD_TILTED'
  | 'HEAD_TURNED'
  | 'TOO_DARK'
  | 'OVEREXPOSED'

export interface SkinSample {
  rgb: [number, number, number]
  hex: string
  /** Luminância média (0–255) das amostras, útil para avaliar a iluminação. */
  luminance: number
}

export interface FaceAnalysis {
  image: { width: number; height: number }
  box: { x: number; y: number; width: number; height: number }
  score: number
  pose: {
    /** Inclinação lateral da cabeça em graus (0 = reta). */
    rollDeg: number
    /** Rotação esquerda/direita: -1 a 1 (0 = de frente). */
    yaw: number
  }
  /** Valores brutos (razões geométricas, independentes do tamanho da foto). */
  ratios: Record<TraitKey, number>
  /** Valores normalizados 0–1, prontos para mapear em sliders de jogos. */
  traits: Record<TraitKey, number>
  faceShape: FaceShape
  skin: SkinSample | null
  warnings: FaceWarning[]
  /** 68 pontos em coordenadas da imagem analisada (úteis para desenhar overlay). */
  landmarks: Point[]
}

export interface AnalyzeOptions {
  /** Lado máximo da imagem usada na análise. Reduz custo em fotos grandes. */
  maxSize?: number
  scoreThreshold?: number
  inputSize?: 160 | 224 | 320 | 416 | 512 | 608
}

/* -------------------------------------------------------------------------- */
/*  Geometria                                                                 */
/* -------------------------------------------------------------------------- */

function dist(a: Point, b: Point): number {
  return Math.hypot(b.x - a.x, b.y - a.y)
}

function mid(a: Point, b: Point): Point {
  return { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 }
}

function avg(points: Point[]): Point {
  const n = points.length || 1
  return {
    x: points.reduce((s, p) => s + p.x, 0) / n,
    y: points.reduce((s, p) => s + p.y, 0) / n,
  }
}

function angleAt(center: Point, a: Point, b: Point): number {
  const v1 = { x: a.x - center.x, y: a.y - center.y }
  const v2 = { x: b.x - center.x, y: b.y - center.y }
  const cos =
    (v1.x * v2.x + v1.y * v2.y) /
    Math.max(Math.hypot(v1.x, v1.y) * Math.hypot(v2.x, v2.y), 1e-6)
  return (Math.acos(Math.min(1, Math.max(-1, cos))) * 180) / Math.PI
}

const clamp01 = (v: number) => Math.min(1, Math.max(0, v))
const round2 = (v: number) => Math.round(v * 100) / 100

/* -------------------------------------------------------------------------- */
/*  Normalização dos traços                                                   */
/* -------------------------------------------------------------------------- */

/**
 * Faixas típicas de cada razão, usadas para converter em 0–1.
 * São pontos de partida: calibre com fotos reais (idealmente um conjunto
 * variado) e ajuste min/max até os extremos dos sliders fazerem sentido.
 */
const TRAIT_RANGES: Record<TraitKey, { min: number; max: number; invert?: boolean }> = {
  faceLength: { min: 1.15, max: 1.6 },
  jawWidth: { min: 0.6, max: 0.85 },
  chinPointiness: { min: 95, max: 150, invert: true }, // ângulo menor = mais pontudo
  eyeSpacing: { min: 0.36, max: 0.5 },
  eyeSize: { min: 0.15, max: 0.24 },
  eyeOpenness: { min: 0.18, max: 0.4 },
  noseWidth: { min: 0.14, max: 0.28 },
  noseLength: { min: 0.2, max: 0.34 },
  mouthWidth: { min: 0.3, max: 0.46 },
  lipFullness: { min: 0.1, max: 0.4 },
}

function normalizeTrait(key: TraitKey, value: number): number {
  const { min, max, invert } = TRAIT_RANGES[key]
  const n = clamp01((value - min) / (max - min))
  return round2(invert ? 1 - n : n)
}

function classifyFaceShape(lengthRatio: number, jawRatio: number): FaceShape {
  if (lengthRatio > 1.45) return 'oblong'
  if (lengthRatio < 1.2) return jawRatio > 0.78 ? 'square' : 'round'
  if (jawRatio < 0.68) return 'heart'
  if (jawRatio > 0.8) return 'square'
  return 'oval'
}

/* -------------------------------------------------------------------------- */
/*  Imagem -> canvas                                                          */
/* -------------------------------------------------------------------------- */

/**
 * Converte qualquer entrada em canvas, respeitando a orientação EXIF
 * (fotos de celular costumam vir "deitadas") e reduzindo o tamanho.
 */
async function toCanvas(input: FaceInput, maxSize: number): Promise<HTMLCanvasElement> {
  let source: CanvasImageSource
  let width: number
  let height: number
  let bitmap: ImageBitmap | null = null

  if (input instanceof Blob) {
    if (!input.type.startsWith('image/')) {
      throw new FaceAnalysisError('INVALID_INPUT', 'Selecione um arquivo de imagem válido.')
    }
    try {
      bitmap = await createImageBitmap(input, { imageOrientation: 'from-image' })
    } catch {
      throw new FaceAnalysisError('INVALID_INPUT', 'Não foi possível ler essa imagem.')
    }
    source = bitmap
    width = bitmap.width
    height = bitmap.height
  } else if (input instanceof HTMLVideoElement) {
    source = input
    width = input.videoWidth
    height = input.videoHeight
  } else if (input instanceof HTMLImageElement) {
    source = input
    width = input.naturalWidth || input.width
    height = input.naturalHeight || input.height
  } else {
    source = input
    width = input.width
    height = input.height
  }

  if (!width || !height) {
    throw new FaceAnalysisError(
      'INVALID_INPUT',
      'A imagem ou o vídeo ainda não está pronto (sem dimensões).',
    )
  }

  const scale = Math.min(1, maxSize / Math.max(width, height))
  const canvas = document.createElement('canvas')
  canvas.width = Math.round(width * scale)
  canvas.height = Math.round(height * scale)

  const ctx = canvas.getContext('2d', { willReadFrequently: true })
  if (!ctx) {
    throw new FaceAnalysisError('INVALID_INPUT', 'Canvas 2D indisponível neste navegador.')
  }

  ctx.drawImage(source, 0, 0, canvas.width, canvas.height)
  bitmap?.close()
  return canvas
}

/* -------------------------------------------------------------------------- */
/*  Tom de pele (aproximado)                                                  */
/* -------------------------------------------------------------------------- */

function median(values: number[]): number {
  const sorted = [...values].sort((a, b) => a - b)
  return sorted[Math.floor(sorted.length / 2)] ?? 0
}

function sampleSkin(
  canvas: HTMLCanvasElement,
  centers: Point[],
  radius: number,
): SkinSample | null {
  const ctx = canvas.getContext('2d', { willReadFrequently: true })
  if (!ctx) return null

  const r: number[] = []
  const g: number[] = []
  const b: number[] = []

  for (const c of centers) {
    const x0 = Math.max(0, Math.round(c.x - radius))
    const y0 = Math.max(0, Math.round(c.y - radius))
    const w = Math.min(canvas.width - x0, radius * 2 + 1)
    const h = Math.min(canvas.height - y0, radius * 2 + 1)
    if (w <= 0 || h <= 0) continue

    const data = ctx.getImageData(x0, y0, w, h).data
    for (let i = 0; i < data.length; i += 4) {
      r.push(data[i])
      g.push(data[i + 1])
      b.push(data[i + 2])
    }
  }

  if (r.length === 0) return null

  const rgb: [number, number, number] = [median(r), median(g), median(b)]
  const hex = '#' + rgb.map((v) => v.toString(16).padStart(2, '0')).join('')
  const luminance = round2(0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2])

  return { rgb, hex, luminance }
}

/* -------------------------------------------------------------------------- */
/*  Análise principal                                                         */
/* -------------------------------------------------------------------------- */

/**
 * Analisa o rosto e devolve traços normalizados (0–1) para criação de personagem.
 * Funciona com upload de foto e também com frames de câmera (passe o <video>).
 */
export async function analyzeFace(
  input: FaceInput,
  options: AnalyzeOptions = {},
): Promise<FaceAnalysis> {
  const { maxSize = 1280, scoreThreshold = 0.4, inputSize = 512 } = options

  await loadModels()
  const canvas = await toCanvas(input, maxSize)

  const detections = await faceapi
    .detectAllFaces(canvas, new faceapi.TinyFaceDetectorOptions({ inputSize, scoreThreshold }))
    .withFaceLandmarks()

  if (detections.length === 0) {
    throw new FaceAnalysisError(
      'NO_FACE',
      'Nenhum rosto foi encontrado. Tente uma foto frontal, nítida e bem iluminada.',
    )
  }

  // Em fotos com mais de um rosto, usa o maior (o mais provável de ser o do usuário).
  const main = detections.reduce((best, d) =>
    d.detection.box.area > best.detection.box.area ? d : best,
  )

  const box = main.detection.box
  const P: Point[] = main.landmarks.positions.map((p) => ({ x: p.x, y: p.y }))

  /*
   * 68 pontos: 0–16 mandíbula | 17–26 sobrancelhas | 27–35 nariz
   *            36–47 olhos    | 48–67 boca
   */

  // Medidas-base. Tudo é dividido por elas, então o resultado não depende
  // da resolução da foto nem do enquadramento do detector (a box varia muito).
  const faceWidth = Math.max(dist(P[0], P[16]), 1)
  const browMid = mid(P[19], P[24])
  // A box dos landmarks não inclui a testa: estimativa heurística do comprimento total.
  const faceLength = dist(P[8], browMid) * 1.45

  const leftEyeCenter = avg(P.slice(36, 42))
  const rightEyeCenter = avg(P.slice(42, 48))

  const leftEyeW = dist(P[36], P[39])
  const rightEyeW = dist(P[42], P[45])
  const leftEyeOpen = (dist(P[37], P[41]) + dist(P[38], P[40])) / (2 * Math.max(leftEyeW, 1))
  const rightEyeOpen = (dist(P[43], P[47]) + dist(P[44], P[46])) / (2 * Math.max(rightEyeW, 1))

  const mouthW = dist(P[48], P[54])

  const ratios: Record<TraitKey, number> = {
    faceLength: faceLength / faceWidth,
    jawWidth: dist(P[4], P[12]) / faceWidth,
    chinPointiness: angleAt(P[8], P[6], P[10]), // em graus
    eyeSpacing: dist(leftEyeCenter, rightEyeCenter) / faceWidth,
    eyeSize: (leftEyeW + rightEyeW) / 2 / faceWidth,
    eyeOpenness: (leftEyeOpen + rightEyeOpen) / 2,
    noseWidth: dist(P[31], P[35]) / faceWidth,
    noseLength: dist(P[27], P[33]) / faceLength,
    mouthWidth: mouthW / faceWidth,
    lipFullness: dist(P[51], P[57]) / Math.max(mouthW, 1),
  }

  const traits = {} as Record<TraitKey, number>
  const roundedRatios = {} as Record<TraitKey, number>
  for (const key of Object.keys(ratios) as TraitKey[]) {
    traits[key] = normalizeTrait(key, ratios[key])
    roundedRatios[key] = round2(ratios[key])
  }

  // Pose: inclinação (roll) pela linha dos olhos; giro (yaw) pela assimetria do nariz.
  const rollDeg =
    (Math.atan2(rightEyeCenter.y - leftEyeCenter.y, rightEyeCenter.x - leftEyeCenter.x) * 180) /
    Math.PI
  const dLeft = dist(P[30], P[1])
  const dRight = dist(P[30], P[15])
  const yaw = (dLeft - dRight) / Math.max(dLeft + dRight, 1)

  // Tom de pele: bochechas + testa (mediana por canal, resistente a brilho/sombras pontuais).
  const eyeMid = mid(leftEyeCenter, rightEyeCenter)
  const forehead = {
    x: browMid.x + (browMid.x - eyeMid.x) * 0.6,
    y: browMid.y + (browMid.y - eyeMid.y) * 0.6,
  }
  const skin = sampleSkin(
    canvas,
    [mid(P[2], P[31]), mid(P[14], P[35]), forehead],
    Math.max(2, Math.round(faceWidth * 0.03)),
  )

  // Avisos de qualidade: a UI pode pedir uma nova foto antes de usar os dados.
  const warnings: FaceWarning[] = []
  if (detections.length > 1) warnings.push('MULTIPLE_FACES')
  if (box.width < 80 || box.width / canvas.width < 0.15) warnings.push('FACE_TOO_SMALL')
  if (box.x < 0 || box.y < 0 || box.x + box.width > canvas.width || box.y + box.height > canvas.height) {
    warnings.push('FACE_CUT_OFF')
  }
  if (main.detection.score < 0.6) warnings.push('LOW_CONFIDENCE')
  if (Math.abs(rollDeg) > 15) warnings.push('HEAD_TILTED')
  if (Math.abs(yaw) > 0.18) warnings.push('HEAD_TURNED')
  if (skin && skin.luminance < 60) warnings.push('TOO_DARK')
  if (skin && skin.luminance > 225) warnings.push('OVEREXPOSED')

  return {
    image: { width: canvas.width, height: canvas.height },
    box: {
      x: Math.round(box.x),
      y: Math.round(box.y),
      width: Math.round(box.width),
      height: Math.round(box.height),
    },
    score: round2(main.detection.score),
    pose: { rollDeg: round2(rollDeg), yaw: round2(yaw) },
    ratios: roundedRatios,
    traits,
    faceShape: classifyFaceShape(ratios.faceLength, ratios.jawWidth),
    skin,
    warnings,
    landmarks: P,
  }
}

/* -------------------------------------------------------------------------- */
/*  Mapeamento para jogos                                                     */
/* -------------------------------------------------------------------------- */

/**
 * Cada jogo descreve seus próprios controles de personalização. Assim o
 * código de análise não muda: só se cria um novo perfil por jogo.
 */
export interface GameSlider {
  id: string // nome do controle no jogo, ex.: "nose_width"
  trait: TraitKey // traço do rosto que alimenta este controle
  min: number // valor mínimo aceito pelo jogo
  max: number // valor máximo aceito pelo jogo
  step?: number // passo do slider (ex.: 1 para inteiros)
  invert?: boolean // inverte a direção, se o jogo usar a escala oposta
}

export interface GameProfile {
  id: string
  name: string
  sliders: GameSlider[]
  /** Preset de formato de rosto do jogo, se existir (ex.: { round: 'face_03' }). */
  faceShapePresets?: Partial<Record<FaceShape, string>>
  /** Se o jogo tem paleta fixa de pele, informe o mapeamento pelo hex mais próximo. */
  skinPalette?: string[]
}

export interface GameCharacterParams {
  gameId: string
  sliders: Record<string, number>
  facePreset?: string
  skinHex?: string
}

function hexToRgb(hex: string): [number, number, number] {
  const h = hex.replace('#', '')
  return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)]
}

function closestColor(target: [number, number, number], palette: string[]): string {
  let best = palette[0]
  let bestDist = Infinity
  for (const hex of palette) {
    const [r, g, b] = hexToRgb(hex)
    const d = (r - target[0]) ** 2 + (g - target[1]) ** 2 + (b - target[2]) ** 2
    if (d < bestDist) {
      bestDist = d
      best = hex
    }
  }
  return best
}

export function mapToGame(analysis: FaceAnalysis, profile: GameProfile): GameCharacterParams {
  const sliders: Record<string, number> = {}

  for (const s of profile.sliders) {
    const t = s.invert ? 1 - analysis.traits[s.trait] : analysis.traits[s.trait]
    let value = s.min + t * (s.max - s.min)
    if (s.step) value = Math.round(value / s.step) * s.step
    sliders[s.id] = round2(Math.min(s.max, Math.max(s.min, value)))
  }

  let skinHex: string | undefined
  if (analysis.skin) {
    skinHex = profile.skinPalette?.length
      ? closestColor(analysis.skin.rgb, profile.skinPalette)
      : analysis.skin.hex
  }

  return {
    gameId: profile.id,
    sliders,
    facePreset: profile.faceShapePresets?.[analysis.faceShape],
    skinHex,
  }
}

/** Exemplo de perfil. Crie um por jogo com os nomes e limites reais dos controles. */
export const EXAMPLE_PROFILE: GameProfile = {
  id: 'exemplo-0-100',
  name: 'Jogo de exemplo (sliders 0–100)',
  sliders: [
    { id: 'face_length', trait: 'faceLength', min: 0, max: 100, step: 1 },
    { id: 'jaw_width', trait: 'jawWidth', min: 0, max: 100, step: 1 },
    { id: 'chin_pointiness', trait: 'chinPointiness', min: 0, max: 100, step: 1 },
    { id: 'eye_spacing', trait: 'eyeSpacing', min: 0, max: 100, step: 1 },
    { id: 'eye_size', trait: 'eyeSize', min: 0, max: 100, step: 1 },
    { id: 'nose_width', trait: 'noseWidth', min: 0, max: 100, step: 1 },
    { id: 'mouth_width', trait: 'mouthWidth', min: 0, max: 100, step: 1 },
    { id: 'lip_fullness', trait: 'lipFullness', min: 0, max: 100, step: 1 },
  ],
  faceShapePresets: { oval: 'face_01', round: 'face_02', square: 'face_03', heart: 'face_04', oblong: 'face_05' },
}
