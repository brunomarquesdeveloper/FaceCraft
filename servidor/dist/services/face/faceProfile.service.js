"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.createFaceProfile = createFaceProfile;
function unavailable() {
    return {
        value: 0,
        available: false,
    };
}
function ratio(numerator, denominator) {
    if (!Number.isFinite(numerator) ||
        !Number.isFinite(denominator) ||
        numerator < 0 ||
        denominator <= 0) {
        return unavailable();
    }
    return {
        value: Number((numerator / denominator).toFixed(5)),
        available: true,
    };
}
function distance(a, b) {
    if (!a || !b)
        return null;
    const values = [a.x, a.y, a.z, b.x, b.y, b.z];
    if (!values.every(Number.isFinite))
        return null;
    return Math.hypot(a.x - b.x, a.y - b.y, a.z - b.z);
}
function buildMeasurements(points) {
    // Índices da topologia facial do MediaPipe.
    // As medidas precisam ser validadas com fotografias reais.
    const faceWidth = distance(points[234], points[454]);
    const faceHeight = distance(points[10], points[152]);
    const leftEyeWidth = distance(points[33], points[133]);
    const rightEyeWidth = distance(points[362], points[263]);
    const eyeSpacing = distance(points[133], points[362]);
    const noseWidth = distance(points[98], points[327]);
    const noseLength = distance(points[168], points[2]);
    const mouthWidth = distance(points[61], points[291]);
    const upperLip = distance(points[13], points[0]);
    const lowerLip = distance(points[14], points[17]);
    const jawWidth = distance(points[172], points[397]);
    const chinLength = distance(points[152], points[17]);
    const safeRatio = (numerator, denominator) => {
        if (numerator === null || denominator === null) {
            return unavailable();
        }
        return ratio(numerator, denominator);
    };
    return {
        faceWidthHeightRatio: safeRatio(faceWidth, faceHeight),
        jawWidthRatio: safeRatio(jawWidth, faceWidth),
        eyeSpacingRatio: safeRatio(eyeSpacing, faceWidth),
        leftEyeWidthRatio: safeRatio(leftEyeWidth, faceWidth),
        rightEyeWidthRatio: safeRatio(rightEyeWidth, faceWidth),
        noseWidthRatio: safeRatio(noseWidth, faceWidth),
        noseLengthRatio: safeRatio(noseLength, faceHeight),
        mouthWidthRatio: safeRatio(mouthWidth, faceWidth),
        upperLipLowerLipRatio: safeRatio(upperLip, lowerLip),
        chinLengthRatio: safeRatio(chinLength, faceHeight),
    };
}
function createFaceProfile(result) {
    if (result.engine !== 'mediapipe-face-landmarker' ||
        !result.image ||
        !Number.isFinite(result.image.width) ||
        !Number.isFinite(result.image.height) ||
        result.image.width <= 0 ||
        result.image.height <= 0 ||
        !Array.isArray(result.landmarks) ||
        result.landmarks.length < 468 ||
        !Number.isInteger(result.faceCount) ||
        result.faceCount < 1 ||
        typeof result.modelVersion !== 'string') {
        throw new Error('O resultado do motor facial é inválido ou incompleto.');
    }
    const measurements = buildMeasurements(result.landmarks);
    const unavailableCount = Object.values(measurements)
        .filter((measurement) => !measurement.available)
        .length;
    const warnings = [
        'As proporções são estimativas dos pontos do modelo, não medidas anatômicas exatas.',
        'A pose, a perspectiva, a iluminação e a oclusão podem afetar os resultados.',
    ];
    if (unavailableCount > 0) {
        warnings.push(`${unavailableCount} medidas não puderam ser calculadas.`);
    }
    return {
        schemaVersion: '1.0.0',
        engine: 'mediapipe-face-landmarker',
        modelVersion: result.modelVersion,
        image: result.image,
        faceCount: result.faceCount,
        landmarkCount: result.landmarks.length,
        measurements,
        quality: {
            status: unavailableCount === 0 ? 'usable' : 'limited',
            warnings,
        },
    };
}
