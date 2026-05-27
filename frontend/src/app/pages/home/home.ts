import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './home.html',
  styleUrl: './home.css'
})
export class Home {
  constructor(
    private router: Router,
    private auth: AuthService
  ) {}

  goToDetection() {
    this.router.navigate(['/dashboard']);
  }

  goToAbout() {
    this.router.navigate(['/about']);
  }

  logout() {
    this.auth.logout();
    this.router.navigate(['/']);
  }
}