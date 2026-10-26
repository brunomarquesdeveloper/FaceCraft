"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.listActiveGames = listActiveGames;
const prisma_1 = require("../lib/prisma");
async function listActiveGames() {
    return prisma_1.prisma.game.findMany({
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
    });
}
