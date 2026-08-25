# Data Mapping y pendientes de validación

| Concepto | Implementación V1 | Estado |
|---|---|---|
| Lead | Salesforce Lead / Candidato | Confirmado por modelo anterior |
| Período académico | `UI_Periodo__c` | Confirmado por modelo anterior |
| Unidad de negocio | `UI_UnidadNegocio__c` | Confirmado por modelo anterior; códigos no catalogados |
| Matrícula | `Status` = Matriculado/Matrícula | Provisional |
| Inscrito | `Status` = Inscrito/Inscripción | Provisional |
| Proyectado | `Status` = Proyectado | Provisional |
| Asesor | `Owner.Name` | Salesforce estándar |
| Grado/Posgrado | filtro manual por `UI_UnidadNegocio__c` | Requiere catálogo de códigos |

## Próxima validación Salesforce
Abrir `SF_ObjectCatalog` y buscar objetos cuyo nombre contenga términos equivalentes a matrícula, inscripción, enrollment, application, admission o student. Si existen, sustituir los mapeos provisionales por relaciones y medidas sobre esos objetos.
