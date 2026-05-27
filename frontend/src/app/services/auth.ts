import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  constructor() {}

  private isBrowser(): boolean {
    return typeof window !== 'undefined' && typeof localStorage !== 'undefined';
  }

  saveUser(user: any) {
    if (this.isBrowser()) {
      localStorage.setItem('user', JSON.stringify(user));
    }
  }

  getUser() {
    if (!this.isBrowser()) {
      return null;
    }

    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }

  logout() {
    if (this.isBrowser()) {
      localStorage.removeItem('user');
    }
  }

  isLoggedIn(): boolean {
    if (!this.isBrowser()) {
      return false;
    }

    return !!localStorage.getItem('user');
  }
}