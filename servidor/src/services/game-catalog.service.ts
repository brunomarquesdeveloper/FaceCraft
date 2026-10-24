import { prisma } from '../lib/prisma'

export async function listActiveGames() {
  return prisma.game.findMany({
    where: {
      active: true,
    },
    select: {
      id: true,
      slug: true,
      name: true,
      active: true,
      createdAt: true,
    },
    orderBy: {
      name: 'asc',
    },
  })
}
