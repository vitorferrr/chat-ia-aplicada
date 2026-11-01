import { DatePipe } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Message } from '../../models/message';
import { ChatService } from '../../services/chat.service';

@Component({
  selector: 'app-chat',
  imports: [FormsModule, DatePipe],
  templateUrl: './chat.html',
  styleUrl: './chat.css',
})
export class Chat {
  private chatService = inject(ChatService);

  messages = signal<Message[]>([]);
  loading = signal(false);
  text = '';

  send() {
    const pergunta = this.text.trim();
    if (!pergunta || this.loading()) return;

    this.messages.update((list) => [...list, { role: 'user', text: pergunta, date: new Date() }]);
    this.text = '';
    this.loading.set(true);

    this.chatService.send(pergunta).subscribe({
      next: (res) => {
        this.messages.update((list) => [...list, { role: 'bot', text: res.resposta, date: new Date() }]);
        this.loading.set(false);
      },
      error: () => {
        this.messages.update((list) => [...list, { role: 'bot', text: 'Erro ao falar com o servidor 😢', date: new Date() }]);
        this.loading.set(false);
      },
    });
  }
}
