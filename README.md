# isu course seat monitor

small python script that checks iowa state’s course search api and sends a discord alert when a seat opens. i fortunately get early registration due to multiple factors. but my friends don't have that fortune - so this is for them. i graduate this semester so finally making this public

i built this so i didn’t have to refresh the schedule of classes all day. it polls the same api the site uses and alerts the moment `unreservedSeats` goes above zero.

---

## what it does

* polls the isu course search api
* checks unreserved seat counts per section
* sends a discord webhook when a seat opens
* exits immediately so you can register

---

## setup

### requirements

* python 3
* `requests`

```bash
pip install requests
```

### configuration

1. create a discord webhook in your server
2. paste the webhook url into `seat_monitor.py`
3. update the course info in the request payload if needed

---

## run

```bash
python seat_monitor.py
````

or run it in the background so it keeps polling even if you close the terminal:

```bash
nohup python seat_monitor.py > seat_monitor.log 2>&1 &
```

you can check logs with:

```bash
tail -f seat_monitor.log
```

stop it with:

```bash
pkill -f seat_monitor.py
```

the script prints current seat counts and sends a discord alert as soon as a seat opens.

---

## future iterations

* make a workday worker that auto signs you up for class (consider working on this, readme reader)
