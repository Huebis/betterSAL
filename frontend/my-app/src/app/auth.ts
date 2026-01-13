import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly UUID_KEY = 'client_uuid';

  setUuid(uuid: string): void {
    localStorage.setItem(this.UUID_KEY, uuid);
  }

  getUuid(): string | null {
    return localStorage.getItem(this.UUID_KEY);
  }

  clearUuid(): void {
    localStorage.removeItem(this.UUID_KEY);
  }

  isLoggedIn(): boolean {
    return !!this.getUuid();
  }
}
