from scanner import RWDScanner
import argparse

def read_csv(source):
    with open(source, 'r') as f:
        websites = [x for x in f.read().split('\n') if x]
    websites = url_normalize(websites)
    return websites

def url_normalize(urls):
    for idx, url in enumerate(urls):
        urls[idx] = urls[idx].strip('"')
        if url.lower()[0:4] != 'http':
            urls[idx] = "http://" + urls[idx]
    return urls

def scan(source, target):
    scanner = RWDScanner()
    websites = read_csv(source)
    with open(target, 'w') as f:
        f.write('input_url,landing_url,retrieve-success,supports-device-width,supports-@media-style,contains-ga-gtm-script\n')
        for website in websites:
            result = scanner.scan(website)
            print(result)
            line = []
            line.append(result['input_url'])
            line.append(result['landing_url'])
            line.append(result['retrieve-success'])
            line.append(result['results']['supports-device-width'])
            line.append(result['results']['supports-@media-style'])
            line.append(result['results']['contains-ga-gtm-script'])
            f.write(','.join([str(x) for x in line]) + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('source', help='source file (CSV)')
    parser.add_argument('target', help='target file (CSV)')
    args = parser.parse_args()
    if args.target:
        scan(args.source, args.target)
    else:
        scan(args.source)