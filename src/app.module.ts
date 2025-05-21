import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { UsuariosModule } from './usuarios/usuarios.module';
import { ExamenesModule } from './examenes/examenes.module';
import { ResultadosModule } from './resultados/resultados.module';
import { HerramientasModule } from './herramientas/herramientas.module';
import { PreguntasModule } from './preguntas/preguntas.module';
import { RespuestasModule } from './respuestas/respuestas.module';
import { ArchivosModule } from './archivos/archivos.module';

@Module({
  imports: [UsuariosModule, ExamenesModule, ResultadosModule, HerramientasModule, PreguntasModule, RespuestasModule, ArchivosModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
