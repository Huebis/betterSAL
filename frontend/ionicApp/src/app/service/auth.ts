import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly UUID_KEY = 'uuid';

  setUuid(uuid: string) {
    localStorage.setItem(this.UUID_KEY, uuid);
  }

  getUuid(): string | null {
    return localStorage.getItem(this.UUID_KEY);
  }

  clearUuid() {
    localStorage.removeItem(this.UUID_KEY);
  }

  isLoggedIn(): boolean {
    return !!this.getUuid();
  }
}
