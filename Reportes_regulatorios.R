#######Separar pipes
A = Compartir_ID_registro_20260930_v7_1_AP %>%
  separate_rows(IdsOrigen, sep = "\\|") %>%
  filter(IdsOrigen != "")
##########################Etiquetado
A$trimestre = "3er trimestre 2026"
A$Tipo = "Accidentes_personales"
######Agrupar pipes
A = A%>%
  group_by(IdsOrigen) %>%
  mutate(valor = paste(ident, collapse = "|"))
get(vars[i]) = rbind(get(vars[i]),A)
