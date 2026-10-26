"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.faceRoutes = void 0;
const faceProfile_service_1 = require("../services/face/faceProfile.service");
const MAX_IMAGE_BYTES = 10 * 1024 * 1024;
const ALLOWED_IMAGE_TYPES = [
    'image/jpeg',
    'image/png',
    'image/webp',
];
const faceRoutes = async (app) => {
    app.addContentTypeParser(ALLOWED_IMAGE_TYPES, {
        parseAs: 'buffer',
        bodyLimit: MAX_IMAGE_BYTES,
    }, (_request, body, done) => {
        done(null, body);
    });
    app.post('/api/face/analyze', { bodyLimit: MAX_IMAGE_BYTES }, async (request, reply) => {
        const contentType = request.headers['content-type']
            ?.split(';')[0]
            ?.trim()
            .toLowerCase();
        if (!contentType ||
            !ALLOWED_IMAGE_TYPES.includes(contentType)) {
            return reply.code(415).send({
                error: 'UNSUPPORTED_IMAGE_TYPE',
                message: 'Envie uma imagem JPEG, PNG ou WebP.',
            });
        }
        const image = request.body;
        if (!Buffer.isBuffer(image) || image.length === 0) {
            return reply.code(400).send({
                error: 'INVALID_IMAGE',
                message: 'Envie uma imagem válida.',
            });
        }
        if (image.length > MAX_IMAGE_BYTES) {
            return reply.code(413).send({
                error: 'IMAGE_TOO_LARGE',
                message: 'A imagem excede o limite de 10 MB.',
            });
        }
        const engineUrl = (process.env.FACE_ENGINE_URL ??
            'http://127.0.0.1:8001').replace(/\/+$/, '');
        try {
            const response = await fetch(`${engineUrl}/analyze`, {
                method: 'POST',
                headers: {
                    'content-type': contentType,
                },
                body: new Uint8Array(image),
                signal: AbortSignal.timeout(60_000),
            });
            let result;
            try {
                result = await response.json();
            }
            catch {
                request.log.error('O motor facial retornou uma resposta inválida.');
                return reply.code(502).send({
                    error: 'INVALID_FACE_ENGINE_RESPONSE',
                    message: 'Resposta inválida do motor facial.',
                });
            }
            if (!response.ok) {
                const status = response.status >= 500
                    ? 502
                    : response.status;
                return reply.code(status).send({
                    error: 'FACE_ANALYSIS_FAILED',
                    message: typeof result.detail === 'string'
                        ? result.detail
                        : 'Não foi possível analisar a imagem.',
                });
            }
            const profile = (0, faceProfile_service_1.createFaceProfile)(result);
            return reply.send({
                ...result,
                profile,
            });
        }
        catch (error) {
            request.log.error({ err: error }, 'Falha ao comunicar com o motor facial.');
            const timedOut = error instanceof Error &&
                error.name === 'TimeoutError';
            return reply.code(timedOut ? 504 : 502).send({
                error: timedOut
                    ? 'FACE_ENGINE_TIMEOUT'
                    : 'FACE_ENGINE_UNAVAILABLE',
                message: timedOut
                    ? 'O motor facial demorou demasiado para responder.'
                    : 'Não foi possível conectar ao motor facial.',
            });
        }
    });
};
exports.faceRoutes = faceRoutes;
