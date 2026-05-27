import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-signup',
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './signup.html',
  styleUrl: './signup.css'
})
export class Signup {
  username = '';
  email = '';
  password = '';
  confirmPassword = '';
  errorMessage = '';
  successMessage = '';
  loading = false;

  constructor(
    private api: ApiService,
    private router: Router
  ) {}

  onSignup() {
    this.errorMessage = '';
    this.successMessage = '';

    if (!this.username || !this.email || !this.password || !this.confirmPassword) {
      this.errorMessage = 'Please fill all fields';
      return;
    }

    if (this.password !== this.confirmPassword) {
      this.errorMessage = 'Passwords do not match';
      return;
    }

    this.loading = true;

    this.api.signup({
      username: this.username,
      email: this.email,
      password: this.password
    }).subscribe({
      next: (response: any) => {
        this.loading = false;
        this.successMessage = response.message || 'User registered successfully';
        setTimeout(() => {
          this.router.navigate(['/']);
        }, 1200);
      },
      error: (error) => {
        this.loading = false;
        this.errorMessage = error?.error?.message || 'Signup failed';
      }
    });
  }
}