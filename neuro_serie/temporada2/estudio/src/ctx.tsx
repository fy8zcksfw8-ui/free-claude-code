import React, {createContext, useContext} from 'react';
import type {ModoRobo} from './personagens';

export type RivalProps = {tamanho: number; boca?: number; modo?: ModoRobo; silhueta?: boolean};
export type Ep = {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  dados: any;
  rivalNome: string; // curto, para placar e etiquetas
  rivalCor: string;
  Rival: React.FC<RivalProps>;
  rodadas: number;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  visuais?: Record<string, React.FC<any>>;
};
const C = createContext<Ep | null>(null);
export const EpProvider: React.FC<{ep: Ep; children: React.ReactNode}> = ({ep, children}) => <C.Provider value={ep}>{children}</C.Provider>;
export const useEp = () => {
  const e = useContext(C);
  if (!e) throw new Error('EpProvider ausente');
  return e;
};
