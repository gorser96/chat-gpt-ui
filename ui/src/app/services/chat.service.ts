import { Inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { AppSettings } from '../models/app.model';
import { APP_CONFIG } from '../app.config';
import { HttpClient } from '@angular/common/http';
import { ChatOut } from '../models/chat.model';

@Injectable({
  providedIn: 'root',
})
export class ChatService {
  _baseUrl: string;

  constructor(
    private httpClient: HttpClient,
    @Inject(APP_CONFIG) config: AppSettings
  ) {
    this._baseUrl = config.apiBaseUrl;
  }

  getChats(): Observable<ChatOut[]> {
    return this.httpClient.get<ChatOut[]>(`${this._baseUrl}chats`, {
      withCredentials: true,
    });
  }
}
