export interface MainCommandResponse {
  id: number;
  name: string
  params: string | null;
  format: string | null;
  data_size: number;
  total_size: number;
}
