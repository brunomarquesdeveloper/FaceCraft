
import assert from 'node:assert/strict'
import test from 'node:test'
import { createFaceProfile } from '../faceProfile.service'

const landmarks = Array.from({ length: 478 }, (_, index) => ({
  x: 0.5 + Math.cos(index) * 0.1,
  y: 0.5 + Math.sin(index) * 0.15,
  z: 0,
}))

test('cria um perfil facial com as medidas esperadas', () => {
  const profile = createFaceProfile({
    engine: 'mediapipe-face-landmarker',
    modelVersion: '1.1.1',
    image: { width: 480, height: 640 },
    faceCount: 1,
    landmarks,
  })

  assert.equal(profile.schemaVersion, '1.0.0')
  assert.equal(profile.landmarkCount, 478)
  assert.equal(profile.quality.status, 'usable')
  assert.equal(
    profile.measurements.faceWidthHeightRatio.available,
    true,
  )
})

test('rejeita um resultado sem pontos suficientes', () => {
  assert.throws(
    () =>
      createFaceProfile({
        engine: 'mediapipe-face-landmarker',
        modelVersion: '1.1.1',
        image: { width: 480, height: 640 },
        faceCount: 1,
        landmarks: [],
      }),
    /inválido ou incompleto/,
  )
})

test('marca medida indisponível quando há coordenadas inválidas', () => {
  const invalidLandmarks = landmarks.map((point) => ({ ...point }))
  invalidLandmarks[234].x = Number.NaN

  const profile = createFaceProfile({
    engine: 'mediapipe-face-landmarker',
    modelVersion: '1.1.1',
    image: { width: 480, height: 640 },
    faceCount: 1,
    landmarks: invalidLandmarks,
  })

  assert.equal(
    profile.measurements.faceWidthHeightRatio.available,
    false,
  )
  assert.equal(profile.quality.status, 'limited')
})