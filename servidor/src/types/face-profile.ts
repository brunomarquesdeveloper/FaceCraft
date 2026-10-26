export type FaceMeasurementName =
  | 'faceWidthHeightRatio'
  | 'jawWidthRatio'
  | 'eyeSpacingRatio'
  | 'leftEyeWidthRatio'
  | 'rightEyeWidthRatio'
  | 'noseWidthRatio'
  | 'noseLengthRatio'
  | 'mouthWidthRatio'
  | 'upperLipLowerLipRatio'
  | 'chinLengthRatio'

export interface NormalizedMeasurement {
  /**
   * Proporção geométrica sem unidade.
   * Não representa diretamente um controle de jogo.
   */
  value: number

  /**
   * Indica se a medida pôde ser calculada com os pontos disponíveis.
   */
  available: boolean
}

export interface FaceMeasurements {
  faceWidthHeightRatio: NormalizedMeasurement
  jawWidthRatio: NormalizedMeasurement
  eyeSpacingRatio: NormalizedMeasurement
  leftEyeWidthRatio: NormalizedMeasurement
  rightEyeWidthRatio: NormalizedMeasurement
  noseWidthRatio: NormalizedMeasurement
  noseLengthRatio: NormalizedMeasurement
  mouthWidthRatio: NormalizedMeasurement
  upperLipLowerLipRatio: NormalizedMeasurement
  chinLengthRatio: NormalizedMeasurement
}

export interface FaceProfile {
  schemaVersion: '1.0.0'
  engine: 'mediapipe-face-landmarker'
  modelVersion: string
  image: {
    width: number
    height: number
  }
  faceCount: number
  landmarkCount: number
  measurements: FaceMeasurements
  quality: {
    status: 'usable' | 'limited'
    warnings: string[]
  }
}