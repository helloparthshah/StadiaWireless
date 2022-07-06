# Stadia Wireless!

Stadia Wireless enables you to use your stadia controller wirelessly. Not just with stadia, but with any game.

## How to use Stadia Wireless

First you need to clone the repository.

Next you need to install the dependencies.

```bash
pip install -r requirements.txt
```
Then first, run the server.

```bash
python controller.py
```

Then you can serve the static files.

I found out browser-sync to work well but you can use any other tool.

```bash
npx browser-sync start --server
```

Access the webite using the external ip address provided by browser-sync on your phone.

Should look like this:
```
[Browsersync] Access URLs:
       Local: http://localhost:3000
    External: http://10.4.51.240:3000
 ------------------------------------
          UI: http://localhost:3001
 UI External: http://localhost:3001
 ------------------------------------
 ```

 Lastly, connect your controller to your phone and enjoy!