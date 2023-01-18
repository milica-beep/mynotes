import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  registerForm!: FormGroup;
  inputType:string = "password";
  
  constructor(private formBuilder: FormBuilder,
              private auth: AuthService) { }

  ngOnInit(): void {
    this.registerForm = this.formBuilder.group({
      name: [''],
      lastname: [''],
      email: ['', Validators.required],
      password: ['', Validators.required]
    })
  }

  get f() { return this.registerForm.controls; }

  onSubmit() {

    if(this.registerForm.invalid) {
      return;
    }

    let name = this.f["name"].value;

    this.auth.register(this.f["name"].value, 
                       this.f["lastname"].value, 
                       this.f["email"].value, 
                       this.f["password"].value)
             .subscribe(
              {
                error: (e) => console.error(e),
                complete: () => console.info('complete') 
              }
            );
  }

}