"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const strict_1 = __importDefault(require("node:assert/strict"));
const node_test_1 = __importDefault(require("node:test"));
const faceProfile_service_1 = require("../faceProfile.service");
const landmarks = Array.from({ length: 478 }, (_, index) => ({
    x: 0.5 + Math.cos(index) * 0.1,
    y: 0.5 + Math.sin(index) * 0.15,
    z: 0,
}));
(0, node_test_1.default)('cria um perfil facial com as medidas esperadas', () => {
    const profile = (0, faceProfile_service_1.createFaceProfile)({
        engine: 'mediapipe-face-landmarker',
        modelVersion: '1.1.1',
        image: { width: 480, height: 640 },
        faceCount: 1,
        landmarks,
    });
    strict_1.default.equal(profile.schemaVersion, '1.0.0');
    strict_1.default.equal(profile.landmarkCount, 478);
    strict_1.default.equal(profile.quality.status, 'usable');
    strict_1.default.equal(profile.measurements.faceWidthHeightRatio.available, true);
});
(0, node_test_1.default)('rejeita um resultado sem pontos suficientes', () => {
    strict_1.default.throws(() => (0, faceProfile_service_1.createFaceProfile)({
        engine: 'mediapipe-face-landmarker',
        modelVersion: '1.1.1',
        image: { width: 480, height: 640 },
        faceCount: 1,
        landmarks: [],
    }), /inválido ou incompleto/);
});
(0, node_test_1.default)('marca medida indisponível quando há coordenadas inválidas', () => {
    const invalidLandmarks = landmarks.map((point) => ({ ...point }));
    invalidLandmarks[234].x = Number.NaN;
    const profile = (0, faceProfile_service_1.createFaceProfile)({
        engine: 'mediapipe-face-landmarker',
        modelVersion: '1.1.1',
        image: { width: 480, height: 640 },
        faceCount: 1,
        landmarks: invalidLandmarks,
    });
    strict_1.default.equal(profile.measurements.faceWidthHeightRatio.available, false);
    strict_1.default.equal(profile.quality.status, 'limited');
});
