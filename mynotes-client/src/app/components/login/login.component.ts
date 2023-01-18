import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm!: FormGroup;
  inputType:string = "password";
  
  constructor(private formBuilder: FormBuilder,
              private auth: AuthService,
              private router: Router) { }

  ngOnInit(): void {
    this.loginForm = this.formBuilder.group({
      email: ['', Validators.required],
      password: ['', Validators.required]
    });
    // this.auth.register("milica", "petkovic", "milicica@elfak.rs", "123456").subscribe(
    //   {
    //     error: (e) => console.error(e),
    //     complete: () => console.info('complete') 
    //   }
    // )
  }

  get f() { return this.loginForm.controls; }

  onSubmit() {
    if (this.loginForm.invalid) {
      return;
    }

    this.auth.login(this.f["email"].value, this.f["password"].value)
      .subscribe(
        {
          error: (e) => console.error(e),
          complete: () => {
            console.info('complete')
            this.router.navigateByUrl('/home');
          }  
        }
      )

  }

}