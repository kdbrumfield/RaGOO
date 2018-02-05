class SeqReader:

    def __init__(self, in_file):
        """
        Initialize sequence file to be parsed.
        :param in_file:
        """
        if not isinstance(in_file, str):
            raise AttributeError('Only a string can be used to instantiate a SeqReader object.')
        self.in_file = in_file

    def parse_fasta(self):
        """
        Generator yielding header and sequence, for each sequence
        in the fasta file sent to the class.
        """
        with open(self.in_file) as fasta_file:
            sequence = ''
            # Find first header.
            line = fasta_file.readline()
            while not line.startswith('>'):
                line = fasta_file.readline()
                if not line:
                    error = """ This file provided is not in proper fasta format.
                    In addition to the usual fasta conventions, be sure that there are
                    no blank lines in the file.
                    """
                    raise RuntimeError(error)
            header = line.rstrip()

            # Get sequence associated with that header.
            for line in fasta_file:
                if line.startswith('>'):
                    # Once the sequence is over, (next header begins),
                    # yield initial header and sequence.
                    yield header, sequence
                    header = line.rstrip()
                    sequence = ''
                else:
                    sequence += ''.join(line.rstrip().split())
        yield header, sequence

    def get_seq(self, in_header):
        in_header = in_header.replace('>', '')
        all_seqs = dict()
        for header, seq in self.parse_fasta():
            all_seqs[header.replace('>', '')] = seq.rstrip()

        return in_header, all_seqs[in_header]