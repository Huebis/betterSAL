import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly UUID_KEY = 'uuid';
  private readonly ROLE_KEY = 'role';

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

  setRole(role:number){
    localStorage.setItem(this.ROLE_KEY,""+role);
  }

  getRole():number{
    let v=localStorage.getItem(this.ROLE_KEY)
    if (v){
      return Number.parseInt(v);
    }else{
      return 0;
    }
   
  }
}
