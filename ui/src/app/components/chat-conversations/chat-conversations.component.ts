import { Component } from '@angular/core';
import { ChatService } from '../../services/chat.service';
import { EMPTY, Observable } from 'rxjs';
import { ChatOut } from '../../models/chat.model';
import { AsyncPipe, NgFor } from '@angular/common';

@Component({
  selector: 'app-chat-conversations',
  standalone: true,
  imports: [NgFor, AsyncPipe],
  templateUrl: './chat-conversations.component.html',
  styleUrl: './chat-conversations.component.css',
})
export class ChatConversationsComponent {
  chats: Observable<ChatOut[]> = EMPTY;

  constructor(private chatServive: ChatService) {}

  ngOnInit() {
    this.chats = this.chatServive.getChats();
  }
}
