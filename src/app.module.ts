import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { ConfigModule } from '@nestjs/config';
import { MongooseModule } from '@nestjs/mongoose';
import { UsuariosModule } from './usuarios/usuarios.module';
import { ResultadosModule } from './resultados/resultados.module';
import { RespuestasModule } from './respuestas/respuestas.module';
import { PreguntasModule } from './preguntas/preguntas.module';
import { HerramientasModule } from './herramientas/herramientas.module';
import { ExamenesModule } from './examenes/examenes.module';
import { ArchivosModule } from './archivos/archivos.module';

@Module({
  imports: [
    UsuariosModule,
    ResultadosModule,
    RespuestasModule,
    PreguntasModule,
    ExamenesModule,
    ArchivosModule,
    HerramientasModule,
    ConfigModule.forRoot({
      isGlobal: true,
    }),
  MongooseModule.forRootAsync({
    imports: [ConfigModule],
    useFactory: async () => ({
      uri: process.env.DB_URI,
    }),
    inject: [],
  }),
],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}