# DecryptionExponentAttack

Per eseguire il codice è necessario avere il file Python `PublicKeyCryptography.py` in quanto verranno invocati dei metodi relativi allo schema RSA. Questo file comunque è già presente nella cartella, quindi non è necessario eseguire nessuna azione particolare in quanto viene importato automaticamente nel codice tramite lo statement:

```python
import PublicKeyCryptography as Rsa
```

Una volta eseguito il codice, l’utente può scegliere tra una lista di funzioni disponibili che vengono stampate a schermo, semplicemente inserendo il numero corrispondente.

![Schermata 2021-05-11 alle 18.52.27.png](https://res.craft.do/user/full/63cec524-c1b6-57b4-8157-df0476f848cb/doc/38F3E494-D23E-4204-B3AC-F14F8DF5026D/4A972123-8F27-4378-A52D-9254AA2ADFD8_2)

Mostriamo dunque adesso una breve descrizione delle seguenti funzioni e cosa richiedono in input.

## 1. Eseguire l'Attacco al Decryption Exponent

Funzione che consente all’utente di eseguire l’algoritmo dell’attacco al *decryption exponen*t in RSA.

All’utente viene richiesto di inserire in input:

- il modulo **n**;
- l’esponente privato **d**;
- l’esponente pubblico **e** (sul quale si basa l’attacco *decryption exponent*).

La funzione dunque restituisce in output i seguenti valori:

- un **fattore** non banale del modulo n;
- il numero totale di **iterazioni** impiegate dall’algoritmo.

Nel codice la funzione che esegue l’algoritmo dell’attacco al decryption exponent in RSA è:

```python
def decryption_exponent_attack(n, d, e):
	'''some code'''
	return [n_factor, iteration]
```

Mentre la funzione che imposta i valori in input è:

```python
def set_decrption_exponential_attack():
	'''some code'''
```

All’interno della funzione che esegue l’algoritmo dell’attacco al *decryption exponent* vengono utilizzati alcuni metodi che erano stati definiti nel modulo **`PublicKeyCryptography.py`** per l’esercizio 3.1. Questi metodi sono i seguenti:

- `extended_euclidean(x, n)`
- `fast_modular_exponentiation(x, m, n)`

### Test di Esempio

![Schermata 2021-05-13 alle 01.50.05.png](https://res.craft.do/user/full/63cec524-c1b6-57b4-8157-df0476f848cb/doc/38F3E494-D23E-4204-B3AC-F14F8DF5026D/EB482192-B522-4792-9CD0-0728A5449B8D_2/Schermata%202021-05-13%20alle%2001.50.05.png)

## 2. Test Decryption Exponent Attack

Funzione che consente all’utente di testare le prestazioni dell’algoritmo per l’attacco al *decryption exponent* in RSA basandosi sulla generazione casuale di un numero **n** di moduli RSA realistici.

All’utente viene richiesto di inserire in input:

- la dimensione **k** in bits dei moduli RSA che verranno generati casualmente durante il test;
- il **numero totale** di moduli RSA che devono esssere generati e testati.

La funzione dunque restituisce in output: i seguenti valori:

- il **numero medio di iterazioni** dell’algoritmo di attacco;
- il **tempo medio di esecuzione** dell’attacco (in secondi);
- la **varianza del tempo di esecuzione** dell’attacco (in secondi al quadrato).

Nel codice la funzione che esegue questo test è:

```python
def set_random_modules_test():
	'''some code'''
```

All'interno di tale funzione viene utilizzato un metodo definito nel modulo `PublicKeyCryptography.py`:

- `generate_rsa_keys(k)`

### Test di Esempio

Per eseguire un test di esempio realistico (ovvero con numeri di grandezza dell’ordine 10^100) sono stati generati casualmente 100 moduli RSA formati ciascuno da 1024 bits.

I risultati ottenuti sono i seguenti:

- **Numero Medio di Iterazioni:** → **1.47**
- **Tempo Medio di Esecuzione:** → **0.019179019927978515** **secondi**
- **Varianza del Tempo di Esecuzione:** → **0.00015982736049240874 secondi^2**

Possiamo dunque notare come l’algoritmo sia molto efficiente nel trovare un fattore non banale del modulo **n** di RSA se si conosce l’esponente privato **d**, riuscendo a mantenere sempre un numero di iterazioni medio minore o uguale a 2. Infatti in questo test di esempio il risultato ottenuto è di 1.47, però anche effettuando altri test con moduli di dimensione diversa si ottiene sempre un numero medio di iterazioni minore o uguale a 2.

