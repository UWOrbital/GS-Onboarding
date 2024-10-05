export interface CommandRequest {
  name: string
  params: string | null
  format: string | null
}

export interface CommandResponse {
  id: number
  name: string
  params: string | null
  format: string | null
  created_on: string
  updated_on: string
}
