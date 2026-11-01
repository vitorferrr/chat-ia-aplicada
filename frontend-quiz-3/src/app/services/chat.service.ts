import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ChatService {
  private http = inject(HttpClient);
  private apiUrl = 'http://localhost:8000/chat';

  private sessionId = crypto.randomUUID();

  send(pergunta: string): Observable<{ resposta: string; session_id: string }> {
    return this.http.post<{ resposta: string; session_id: string }>(this.apiUrl, {
      pergunta,
      session_id: this.sessionId,
    });
  }
}
