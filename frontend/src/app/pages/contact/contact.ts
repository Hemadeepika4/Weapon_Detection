import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-contact',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './contact.html',
  styleUrl: './contact.css'
})
export class Contact {
  constructor(
    private router: Router,
    private auth: AuthService
  ) {}

  logout() {
    this.auth.logout();
    this.router.navigate(['/']);
  }
}