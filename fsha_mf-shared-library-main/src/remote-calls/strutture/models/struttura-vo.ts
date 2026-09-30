export interface StrutturaVO {
  key: number;
  nmTabella: string;
  nmColonna: string;
  dsValore: string;
  dsVisibilita: string;
  dsBreve: string;
  idDipendenza: number | null;
  dipendenza: StrutturaVO | null;
}
