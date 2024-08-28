import redis from 'redis';
import kue from 'kue';
import express from 'express';
import { promisify } from 'util';

const client = redis.createClient();
const get = promisify(client.get).bind(client);
const set = promisify(client.set).bind(client);

const reserveSeat = async (number) => await set('available_seats', number);

const getCurrentAvailableSeats = async () => {
  return await get('available_seats');
};

let reservationEnabled;

const queue = kue.createQueue();

const process = async () => {
  queue.process('reserve_seat', async (job, done) => {
    let seats = await getCurrentAvailableSeats();

    if (seats <= 0) {
      done(Error('Not enough seats available'));
    } else {
      await reserveSeat(seats - 1);
      seats = await getCurrentAvailableSeats();

      if (seats <= 0) reservationEnabled = false;

      done();
    }
  });
};

const app = express();

app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.send(JSON.stringify({ numberOfAvailableSeats }));
});

app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    res
      .status(403)
      .send(JSON.stringify({ status: 'Reservations are blocked' }));
    return;
  }

  const newJob = queue.create('reserve_seat', {}).save((err) => {
    if (err) {
      res.status(500).send(JSON.stringify({ status: 'Reservations failed' }));
      return;
    }
    res.send(JSON.stringify({ status: 'Reservation in process' }));
  });

  newJob.on('failed', (err) =>
    console.log(`Seat reservation job ${newJob.id} failed: ${err}`)
  );

  newJob.on('complete', () =>
    console.log(`Seat reservation job ${newJob.id} completed`)
  );
});

app.get('/process', (req, res) => {
  process().then(() =>
    res.send(
      JSON.stringify({
        status: 'Queue processing',
      })
    )
  );
});

app.listen(1245, () => {
  reserveSeat(50);
  reservationEnabled = true;
});
