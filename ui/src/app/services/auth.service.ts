import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
import { Observable, catchError, mergeMap, of, tap } from 'rxjs';
import { IAuthUser, IUser } from '../models/user.model';
import { CookieService } from 'ngx-cookie-service';
import { AppSettings } from '../models/app.model';
import { APP_CONFIG } from '../app.config';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  _baseUrl: string;
  _storageKey: string = 'authUser';

  constructor(
    private httpClient: HttpClient,
    private cookieService: CookieService,
    @Inject(APP_CONFIG) config: AppSettings
  ) {
    this._baseUrl = config.apiBaseUrl;
  }

  isLoggedIn() {
    console.log('isLoggedIn');
    return localStorage.getItem(this._storageKey) !== null;
  }

  getAuthUser(): IUser | null {
    const user = localStorage.getItem(this._storageKey);
    if (!!user) {
      return JSON.parse(user);
    }
    return null;
  }

  logout() {
    console.log('logout');
    localStorage.removeItem(this._storageKey);
    this.cookieService.delete('user-token');
  }

  login(data: IAuthUser): Observable<IUser> {
    console.log('login');
    const formData = new FormData();
    formData.append('username', data.username + '@test.com');
    formData.append('password', data.password);
    return this.httpClient
      .post<void>(`${this._baseUrl}auth/login`, formData, {
        withCredentials: true,
      })
      .pipe(
        mergeMap(() =>
          this.get_current_user().pipe(
            tap((result) => {
              localStorage.setItem(this._storageKey, JSON.stringify(result));
            })
          )
        )
      );
  }

  verify_authorization(): Observable<IUser> {
    return this.get_current_user().pipe(
      catchError((err) => {
        this.logout();
        return of();
      }),
      tap((result) => {
        localStorage.setItem(this._storageKey, JSON.stringify(result));
      })
    );
  }

  get_current_user(): Observable<IUser> {
    console.log('get_current_user');
    return this.httpClient.get<IUser>(`${this._baseUrl}current-user`, {
      withCredentials: true,
    });
  }
}
