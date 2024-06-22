export interface ChatOut {
  chat_id: string
  user_id: string
  model: string
  messages: ChatMessageOut[]
  created_at: Date
  updated_at: Date
}

export interface ChatMessageOut {
  role: string
  content: string
}