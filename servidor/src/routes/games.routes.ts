import type { FastifyInstance } from 'fastify'
import { listActiveGames } from '../services/game-catalog.service'

export async function gamesRoutes(app: FastifyInstance) {
  app.get('/api/games', async (_request, reply) => {
    try {
      const games = await listActiveGames()

      return reply.status(200).send({
        data: games,
      })
    } catch (error) {
      app.log.error(error, 'Erro ao consultar catálogo de jogos')

      return reply.status(500).send({
        error: 'Não foi possível consultar o catálogo de jogos.',
      })
    }
  })
}
