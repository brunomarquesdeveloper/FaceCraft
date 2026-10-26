"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
require("dotenv/config");
const fastify_1 = __importDefault(require("fastify"));
const cors_1 = __importDefault(require("@fastify/cors"));
const games_routes_1 = require("./routes/games.routes");
const app = (0, fastify_1.default)({
    logger: true,
});
async function start() {
    await app.register(cors_1.default, {
        origin: process.env.APP_ORIGIN ?? 'http://localhost:5173',
    });
    app.get('/api/health', async () => ({
        status: 'ok',
        service: 'FaceCraft API',
    }));
    await app.register(games_routes_1.gamesRoutes);
    try {
        await app.listen({
            port: Number(process.env.PORT ?? 3000),
            host: '0.0.0.0',
        });
    }
    catch (error) {
        app.log.error(error);
        process.exit(1);
    }
}
start();
