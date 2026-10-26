"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
require("dotenv/config");
const prisma_1 = require("./lib/prisma");
async function main() {
    try {
        await prisma_1.prisma.$connect();
        const result = await prisma_1.prisma.$queryRaw `SELECT current_database()`;
        console.log('Conexão com Neon estabelecida!');
        console.log('Banco conectado:', result[0]?.current_database);
    }
    catch (error) {
        console.error('Falha na conexão com Neon:', error);
        process.exitCode = 1;
    }
    finally {
        await prisma_1.prisma.$disconnect();
    }
}
main();
