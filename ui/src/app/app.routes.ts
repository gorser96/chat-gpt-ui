import { Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { authGuard, loggedInGuard } from './services/auth.guard';
import { ChatPageComponent } from './components/chat-page/chat-page.component';

export const routes: Routes = [
  { path: 'login', component: LoginComponent, canActivate: [loggedInGuard] },
  { path: '**', component: ChatPageComponent, canActivate: [authGuard] },
];
