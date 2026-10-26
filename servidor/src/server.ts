import 'dotenv/config'
import Fastify from 'fastify'
import cors from '@fastify/cors'
import { gamesRoutes } from './routes/games.routes'
import { faceRoutes } from './routes/face.routes'

const app = Fastify({
  logger: true,
})

async function start() {
  await app.register(cors, {
    origin: process.env.APP_ORIGIN ?? 'http://localhost:5173',
  })

  app.get('/api/health', async () => ({
    status: 'ok',
    service: 'FaceCraft API',
  }))

  await app.register(gamesRoutes)
  await app.register(faceRoutes)

  try {
    await app.listen({
      port: Number(process.env.PORT ?? 3000),
      host: '0.0.0.0',
    })
  } catch (error) {
    app.log.error(error)
    process.exit(1)
  }
}

start()