import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-about',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './about.html',
  styleUrl: './about.css'
})
export class About {
  constructor(
    private router: Router,
    private auth: AuthService
  ) {}

  logout() {
    this.auth.logout();
    this.router.navigate(['/']);
  }
}