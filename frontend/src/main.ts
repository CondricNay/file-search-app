import { createApp } from 'vue'
import App from './App.vue'

// PrimeVue
import PrimeVue from 'primevue/config'
import FileUpload from 'primevue/fileupload'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import Card from 'primevue/card'
import ToastService from 'primevue/toastservice'
import Toast from 'primevue/toast'

import 'primeicons/primeicons.css';

const app = createApp(App);

app.use(ToastService);

app.component('FileUpload', FileUpload);
app.component('InputText', InputText);
app.component('Button', Button);
app.component('Card', Card);
app.component('Toast', Toast);

app.mount('#app');
