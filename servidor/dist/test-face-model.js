"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tasks_vision_1 = require("@mediapipe/tasks-vision");
const canvas_1 = require("@napi-rs/canvas");
const node_path_1 = require("node:path");
const imageUrl = 'https://img.magnific.com/fotos-gratis/retrato-de-homem-branco-isolado_53876-40306.jpg?semt=ais_hybrid&w=740&q=80';
async function main() {
    console.log('1. Baixando imagem...');
    const response = await fetch(imageUrl, {
        signal: AbortSignal.timeout(15000),
    });
    if (!response.ok) {
        throw new Error(`Falha no download: HTTP ${response.status}`);
    }
    const contentType = response.headers.get('content-type') ?? '';
    if (!contentType.toLowerCase().startsWith('image/')) {
        throw new Error(`Conteúdo não é imagem: ${contentType}`);
    }
    const bytes = Buffer.from(await response.arrayBuffer());
    if (bytes.length > 10 * 1024 * 1024) {
        throw new Error('Imagem excede o limite de 10 MB');
    }
    console.log(`Imagem recebida: ${bytes.length} bytes`);
    console.log('2. Decodificando imagem...');
    const image = await (0, canvas_1.loadImage)(bytes);
    const canvas = (0, canvas_1.createCanvas)(image.width, image.height);
    const context = canvas.getContext('2d');
    context.drawImage(image, 0, 0);
    console.log(`Dimensões: ${image.width}x${image.height}`);
    console.log('3. Carregando runtime do MediaPipe...');
    const wasmPath = (0, node_path_1.resolve)(process.cwd(), 'node_modules/@mediapipe/tasks-vision/wasm');
    const vision = await tasks_vision_1.FilesetResolver.forVisionTasks(wasmPath);
    console.log('4. Carregando Face Landmarker...');
    const modelPath = (0, node_path_1.resolve)(process.cwd(), 'models/face_landmarker.task');
    const landmarker = await tasks_vision_1.FaceLandmarker.createFromOptions(vision, {
        baseOptions: {
            modelAssetPath: modelPath,
        },
        runningMode: 'IMAGE',
        numFaces: 1,
        outputFaceBlendshapes: true,
        outputFacialTransformationMatrixes: true,
    });
    console.log('5. Analisando rosto...');
    try {
        const result = landmarker.detect(canvas);
        console.log('Rostos detectados:', result.faceLandmarks.length);
        if (result.faceLandmarks.length > 0) {
            console.log('Pontos faciais:', result.faceLandmarks[0].length);
            console.log('Categorias de expressão:', result.faceBlendshapes?.[0]?.categories.length ?? 0);
            console.log('Matriz de transformação disponível:', Boolean(result.facialTransformationMatrixes?.length));
            console.log('Primeiros pontos:', JSON.stringify(result.faceLandmarks[0].slice(0, 3), null, 2));
        }
        else {
            console.log('Nenhum rosto detectado nesta imagem.');
        }
    }
    finally {
        landmarker.close();
    }
}
main().catch((error) => {
    console.error('Falha no teste facial:');
    if (error instanceof Error) {
        console.error(error.stack ?? error.message);
    }
    else {
        console.error(error);
    }
    process.exitCode = 1;
});
