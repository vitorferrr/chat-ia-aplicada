export interface Message {
  role: 'user' | 'bot';
  text: string;
  date: Date;
}
