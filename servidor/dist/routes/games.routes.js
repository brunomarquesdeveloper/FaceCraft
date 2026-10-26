"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.gamesRoutes = gamesRoutes;
const game_catalog_service_1 = require("../services/game-catalog.service");
async function gamesRoutes(app) {
    app.get('/api/games', async (_request, reply) => {
        try {
            const games = await (0, game_catalog_service_1.listActiveGames)();
            return reply.status(200).send({
                data: games,
            });
        }
        catch (error) {
            app.log.error(error, 'Erro ao consultar catálogo de jogos');
            return reply.status(500).send({
                error: 'Não foi possível consultar o catálogo de jogos.',
            });
        }
    });
}
