import 'dotenv/config'
import { prisma } from './lib/prisma'

async function main() {
  try {
    await prisma.$connect()

    const result = await prisma.$queryRaw<
      Array<{ current_database: string }>
    >`SELECT current_database()`

    console.log('Conexão com Neon estabelecida!')
    console.log('Banco conectado:', result[0]?.current_database)
  } catch (error) {
    console.error('Falha na conexão com Neon:', error)
    process.exitCode = 1
  } finally {
    await prisma.$disconnect()
  }
}

main()