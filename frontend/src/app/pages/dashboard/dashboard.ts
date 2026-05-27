import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { ApiService } from '../../services/api';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css'
})
export class Dashboard implements OnInit {

  username = 'User';
  user: any = null;

  imageFile: File | null = null;
  videoFile: File | null = null;

  imagePreview: string | null = null;
  videoPreview: string | null = null;

  imageResult: any = null;
  videoResult: any = null;
  cameraResult: any = null;

  imageLoading = false;
  videoLoading = false;
  cameraLoading = false;

  imageError = '';
  videoError = '';
  cameraError = '';

  cameraStarted = false;
  private cameraStream: MediaStream | null = null;

  showAlert = false;
  alertTitle = '';
  alertMessage = '';

  @ViewChild('cameraVideo') cameraVideoRef!: ElementRef<HTMLVideoElement>;

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
  }

  logout() {
    this.stopCamera();
    this.auth.logout();
    this.router.navigate(['/']);
  }

  goToHistory() {
    this.router.navigate(['/history']);
  }

  onImageSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (!input.files?.length) return;

    this.imageFile = input.files[0];
    this.imageError = '';
    this.imageResult = null;

    const reader = new FileReader();
    reader.onload = () => {
      this.imagePreview = reader.result as string;
    };
    reader.readAsDataURL(this.imageFile);
  }

  onVideoSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (!input.files?.length) return;

    this.videoFile = input.files[0];
    this.videoError = '';
    this.videoResult = null;

    this.videoPreview = URL.createObjectURL(this.videoFile);
  }

  detectImage() {
    if (!this.imageFile || !this.user?.id) {
      this.imageError = 'Please choose an image first';
      return;
    }

    this.imageLoading = true;

    const formData = new FormData();
    formData.append('file', this.imageFile);
    formData.append('user_id', String(this.user.id));

    this.api.detectImage(formData).subscribe({
      next: (res: any) => {
        this.imageLoading = false;
        this.imageResult = res;
        this.checkForAlerts(res?.detections || []);
      },
      error: (err) => {
        this.imageLoading = false;
        this.imageError = err?.error?.message || 'Image detection failed';
      }
    });
  }

  detectVideo() {
    if (!this.videoFile || !this.user?.id) {
      this.videoError = 'Please choose a video first';
      return;
    }

    this.videoLoading = true;

    const formData = new FormData();
    formData.append('file', this.videoFile);
    formData.append('user_id', String(this.user.id));

    this.api.detectVideo(formData).subscribe({
      next: (res: any) => {
        this.videoLoading = false;
        this.videoResult = res;
        this.checkForAlerts(res?.detections || []);
      },
      error: (err) => {
        this.videoLoading = false;
        this.videoError = err?.error?.message || 'Video detection failed';
      }
    });
  }

  startCamera() {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then((stream) => {
        this.cameraStream = stream;
        this.cameraStarted = true;
        this.cameraVideoRef.nativeElement.srcObject = stream;
      })
      .catch(() => {
        this.cameraError = 'Unable to access camera';
      });
  }

  stopCamera() {
    this.cameraStream?.getTracks().forEach(track => track.stop());
    this.cameraStream = null;

    if (this.cameraVideoRef?.nativeElement) {
      this.cameraVideoRef.nativeElement.srcObject = null;
    }

    this.cameraStarted = false;
  }

  captureFrame() {
    if (!this.cameraStarted || !this.user?.id) {
      this.cameraError = 'Start camera first';
      return;
    }

    const video = this.cameraVideoRef.nativeElement;
    const canvas = document.createElement('canvas');

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.drawImage(video, 0, 0);

    this.cameraLoading = true;

    canvas.toBlob((blob) => {
      if (!blob) return;

      const formData = new FormData();
      formData.append('file', blob, 'frame.jpg');
      formData.append('user_id', String(this.user.id));

      this.api.detectImage(formData).subscribe({
        next: (res: any) => {
          this.cameraLoading = false;
          this.cameraResult = res;
          this.checkForAlerts(res?.detections || []);
        },
        error: () => {
          this.cameraLoading = false;
          this.cameraError = 'Camera detection failed';
        }
      });
    });
  }

  checkForAlerts(detections: any[]) {
    if (!detections?.length) {
      this.showAlert = false;
      return;
    }

    const danger = detections.find(
      (d: any) => d.threat === 'HIGH' || d.threat === 'VERY HIGH'
    );

    if (danger) {
      this.alertTitle = '🚨 HIGH THREAT DETECTED';
      this.alertMessage = `${danger.class_name} (${danger.confidence}) - ${danger.threat}`;
      this.showAlert = true;

      setTimeout(() => {
        this.showAlert = false;
      }, 10000);
    } else {
      this.showAlert = false;
    }
  }

  closeAlert() {
    this.showAlert = false;
  }

  getImageOutputUrl(path: string) {
    return `http://127.0.0.1:5000${path}`;
  }

  getVideoOutputUrl(path: string) {
    return `http://127.0.0.1:5000${path}`;
  }
}