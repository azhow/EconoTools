#!/usr/bin/env python3
import requests
import re
import argparse

def is_float_try(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

def get_selic(num):
    link = 'https://www.bcb.gov.br/Pec/Copom/Port/taxaSelic.asp'
    f = requests.get(link)
    text = f.text
    text = text.splitlines()
    nt = []
    lout = []

    for line in text:
        nt.append(line.strip())

    if num > len(nt):
        raise ValueError("Série requisitada é maior que a disponível.")

    for i in range(len(nt)-1):
        if len(lout) < num:
            nt[i+1] = nt[i+1].replace(',','.')
            m = re.search("<TD>[0-3][0-9]/[0-1][0-9]/[1-2][0-9][0-9][0-9]</TD>", nt[i])
            if m:
                txt = m.group(0)[4:14]
            if nt[i] == '<TD class="fundoPadraoBEscuro3 centralizado">' and i%2 == 0 \
            and is_float_try(nt[i+1]):
                lout.append((txt, nt[i+1]))

    return lout

def main(num):
    lin = get_selic(num)

    arquivo = open("data.dat", 'w')
    arquivo.write("#DATA\tTAXA\n")
    for info in lin:
        write = info[0] + ' ' + info[1] + '\n'
        arquivo.write(write)
    arquivo.close()

if __name__ == '__main__':
    prs = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                  description="Script para pegar o histórico da taxa SELIC.")
    prs.add_argument('-n', "--numero", type=int, default=10, help="Numero de amostras da série histórica.")

    args = prs.parse_args()
    main(args.numero)
