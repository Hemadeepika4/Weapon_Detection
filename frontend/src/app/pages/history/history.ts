import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { ApiService } from '../../services/api';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-history',
  imports: [CommonModule],
  templateUrl: './history.html',
  styleUrl: './history.css'
})
export class History implements OnInit {
  user: any = null;
  username = 'User';
  uploads: any[] = [];
  loading = true;
  errorMessage = '';

  constructor(
    private router: Router,
    private api: ApiService,
    private auth: AuthService
  ) {}

  ngOnInit(): void {
    const savedUser = this.auth.getUser();

    if (!savedUser) {
      this.router.navigate(['/']);
      return;
    }

    this.user = savedUser;
    this.username = savedUser.username || 'User';
    this.loadUploads();
  }

  loadUploads() {
    this.loading = true;
    this.errorMessage = '';

    this.api.getUploads(this.user.id).subscribe({
      next: (response: any) => {
        this.loading = false;
        this.uploads = response.uploads || [];
      },
      error: (error) => {
        this.loading = false;
        this.errorMessage = error?.error?.message || 'Failed to load upload history';
      }
    });
  }

  goToDashboard() {
    this.router.navigate(['/dashboard']);
  }

  logout() {
    this.auth.logout();
    this.router.navigate(['/']);
  }

  getFileUrl(path: string) {
  if (!path) return '';

  const normalizedPath = path.replace(/\\/g, '/').replace(/^\/+/, '');
  return `http://127.0.0.1:5000/${normalizedPath}`;
 }
  isImage(fileType: string) {
    return fileType?.toLowerCase() === 'image';
  }

  isVideo(fileType: string) {
    return fileType?.toLowerCase() === 'video';
  }
}