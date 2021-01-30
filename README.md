# SplendidReads
A simple e-book store created using python's Django framework.

## Description
* **SplendidReads** is a simple e-book store can be used by anyone.
* The website provides user authentication and authorization features which ensures that legitimate users access the website services.
* Currently, the only payment currency accepted is '**Indian Rupee**' (INR).
* The website uses '**Razorpay**' as the payment gateway. For more details visit https://razorpay.com/.<br> **Note:** This is a demo website, hence, the payment portal runs in **test mode**.
  No real money is deducted from a user's account.
* Since the website is a demo website, the products are not real due to copyright issues. The website does not also provide an e-book reader. However, an e-book reader will be integrated in the future, but the products will still be samples.
* The product data used on this website has been obtained from https://github.com/uchidalab/book-dataset.


## Screenshots
![Home page](/static/images/home.png)
<br>
![Genres page](/static/images/genres.png)
<br>
![Product details page](/static/images/product_details.png)
<br>
![Cart page](/static/images/cart.png)
<br>
![SignUp page](/static/images/signup.png)
<br>
![SignIn page](/static/images/signin.png)
<br>
![Payment page](/static/images/payment.png)

## Requirements
* python 3.9.0
* django 3.1.5
* razorpay 1.2.0

## How to Use?
 #### Project Setup  
1. (**Skip this step if you already have the required version**)Install Python.

1. Clone the project from the project repo
   >$git clone https://github.com/TheRevenant04/SplendidReads.

1. (**Optional but recommended**) Create a virtual environment in the project folder. Replace **name** with a name you of your choice.
   >(path to your project)$python -m venv **name**  

1. (**Skip this step if you skipped the previous step**)Activate the virtual environment. Replace **name** with **name** from the previous step.
   >(path to your project)$**name**\scripts\activate

1. Install the required packages.
   >(path to your project)$pip install -r requirements.txt

1. Create the project database.
   >(path to your project)$python manage.py migrate

1. Load product details in the database.
   >(path to your project)$python manage.py shell

   >$exec(open("./load_product_data.py").read())

   This will take a while to execute.

1. Run the project.
   >(path to your project)$python manage.py runserver

1. Open a browser and enter the following URL
   >127.0.0.1:8000
  #### Project Configuration
The project is configured to use the **gmail mailserver** for sending emails to users. If you wish to use this configuration, fill your gmail email address in the **EMAIL_HOST_USER** and password in the **EMAIL_HOST_PASSWORD** in the **SplendidReads/settings.py** file(This configuration also works on localhost provided you are connected to the internet). The code looks like this in the settings.py file:
>EMAIL_USE_TLS = True<br>
EMAIL_HOST = "smtp.gmail.com"<br>
EMAIL_HOST_USER = "Your EMAIL ID"<br>
EMAIL_HOST_PASSWORD = "Your EMAIL PASSWORD"<br>
EMAIL_PORT = 587

However, if you are running the project on your local machine and dont wish to use the gmail mailserver then you can comment the following lines in the 'settings.py' file
>EMAIL_USE_TLS = True<br>
EMAIL_HOST = "smtp.gmail.com"<br>
EMAIL_HOST_USER = "Your EMAIL ID"<br>
EMAIL_HOST_PASSWORD = "Your EMAIL PASSWORD"<br>
EMAIL_PORT = 587

and add the following line in the 'settings.py' file.

>EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

To use the payment gateway on the website a **KEY ID** and a **KEY SECRET** is required for the payment API.
This requires a merchant to create an account with **Razorpay**. The procedure can be found here, https://razorpay.com/docs/payment-gateway/dashboard-guide/sign-up/.
Follow the process only till '**Verify Email Address**'.<br><br>
The API keys can be generated and obtained by following this https://razorpay.com/docs/payment-gateway/dashboard-guide/settings/api-keys/.

On obtaining the API keys the following changes need to be made:
1. In the **Payments/views.py** replace,
   >client = razorpay.Client(auth=("Your KEY ID", "Your KEY SECRET"))

   with the API keys you obtained from Razorpay.

1. In the **Payments/templates/Payments/checkout_page.html** replace,
   >data-key="Your API key"

   with your API **KEY ID** obtained from Razorpay.

 ## Disclaimer
 The product details used in this project are a copyright of Amazon Inc. However the use of this data is purely for academic purpose and not for any commercial use.
