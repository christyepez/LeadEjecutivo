# LeadEjecutivo — Power BI PBIP / PBIR

Panel ejecutivo de evolución de Leads para Universidad Indoamérica. La solución reutiliza la arquitectura conceptual del proyecto `PanelLeadsIndo` y conserva Salesforce como origen.

## Objetivo
Narrar el journey comercial desde captación hasta matrícula, con vistas específicas de Grados, Posgrados y desempeño de asesores.

## Hojas
1. **Resumen Ejecutivo - Journey**: tarjetas Leads, Proyectados, Inscritos, Matrículas y Matrículas YTD; funnel por estado; evolución temporal; matrículas por período; ranking por carrera.
2. **Grados**: orígenes, campañas/canales, carreras, perdidos, ranking, matrículas y backlog sin actividad.
3. **Posgrados**: misma lógica analítica, separable mediante `UI_UnidadNegocio__c`.
4. **Asesores**: carga, gestión, pérdida, matrícula, inactividad 7/30 días y matriz de desempeño.

## Fuente y modelo
- Salesforce OAuth2: `https://login.salesforce.com/`.
- Lead → `Candidato`.
- LeadHistory → `Historial de candidatos`.
- Opportunity → `Oportunidad`.
- Dimensiones: Fecha, Sede, Carrera, Modalidad.
- `SF_ObjectCatalog` expone el catálogo de objetos disponible en la conexión para facilitar el descubrimiento de objetos de matrícula/inscripción/proyección.

## Advertencia de gobierno
Los KPIs `Total Matriculas`, `Total Inscritos` y `Total Proyectados` usan inicialmente un mapeo por `Candidato[Status]`. Este mapeo es deliberadamente explícito y está marcado como **provisional**. Debe reemplazarse por objetos/campos dedicados si Salesforce contiene entidades transaccionales de matrícula o inscripción. No se inventaron nombres de objetos custom.

## Períodos académicos
Se usa `UI_Periodo__c` como filtro académico y `DimFecha[Date]` como filtro temporal. Las medidas YTD respetan el contexto de fecha.

## Grado / Posgrado
No se hardcodean códigos de `UI_UnidadNegocio__c`. Cada página incluye el slicer de Unidad de negocio para seleccionar los valores reales de Salesforce. Una vez confirmado el catálogo de códigos se puede fijar el filtro de página.

## Ejecución
Abra `LeadEjecutivo.pbip` con Power BI Desktop, autentique Salesforce mediante OAuth2 y revise primero `SF_ObjectCatalog` en Power Query para validar si existen objetos específicos de matrícula/inscripción.
