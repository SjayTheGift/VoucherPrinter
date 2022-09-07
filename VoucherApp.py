class VoucherPrinter():

    def print_vouchers(self, vouchers, output_file):
        # use the line_items and voucher objects
        if output_file:
            columns = int(headers.get('columns'))
            # seed the loop
            next_vouchers = self.get_items_to_print(columns, vouchers)
            while len(next_vouchers) > 0:
                # items are vertical
                for line in line_items:
                    # iterate through each voucher and print the field value
                    for i in range(len(next_vouchers)):
                        voucher = next_vouchers[i]
                        field = voucher.get(line)
                        if line == 'empty':
                            field = ' '
                        # column left padding
                        output_file.write(' ' * int(headers.get('left_margin')))
                        # create set widths
                        # write the data
                        output_file.write(field)
                        field_with_spacing = ' ' * (int(headers.get('column_width')) - len(field))
                        output_file.write(field_with_spacing)
                        # space the columns
                        column_spacing = ' ' * int(headers.get('column_spacing'))
                        output_file.write(column_spacing)
                    output_file.write('\n')

                # space the rows
                row_spacing = '\n' * int(headers.get('row_spacing'))
                # get new items
                next_vouchers = self.get_items_to_print(columns, vouchers)
                if len(next_vouchers) > 0:
                    output_file.write(row_spacing)
                else:
                    output_file.close()
                    break
        print('Results complete priting')

    def get_items_to_print(self, columns, items):
        if len(items) == 0:
            response = []
        elif columns > len(items):
            response = [items.pop(0) for i in range(len(items))]
        else:
            response = [items.pop(0) for i in range(columns)]
        return response

    def aggregate_voucher(self, voucher):
        name = voucher.get('description')
        if name in voucher_averages:
            count = voucher_averages.get(name)
            count += 1
            voucher_averages[name] = count
        else:
            voucher_averages[name] = 1


    def create_voucher(self, headers, voucher_data):
        # if the lengths are not equal, format will be incorrect
        # print(voucher_data)
        voucher_data = [data.rstrip('\r\n') for data in voucher_data]
        return dict(zip(headers, voucher_data))

    def validate(self, vouchers, voucher_values, file_input_path):

        if(int(len(vouchers)) == int(voucher_values)):
            print('\nFile successfully passed file validation, summary matches vouchers\n')
            last_stop = file_input_path.rfind(".")
            output_file = file_input_path[:last_stop] + '_result.txt'
            output_file = open(output_file, 'w')
            self.print_vouchers(vouchers, output_file)
        else:
            raise Exception('\nValidation Error: File failed validation, vouchers did not match summary.\n')
            

    def main(self, file_input_path):
        input_file = open(file_input_path, 'r')
        are_vouchers = False
        line = input_file.readline().rstrip('\r\n')
        voucher_values = 0
        while line:
            if are_vouchers:
                if headers.get('voucher_fields'):
                    voucher = self.create_voucher(headers.get('voucher_fields'), line.split(','))
                    self.aggregate_voucher(voucher)
                    vouchers.append(voucher)
            else:
                line_splt = line.split(':')
                if line_splt[0] == 'line_item':
                    # Dynamically build the formatter
                    line_items.append(line_splt[1])
                elif line_splt[0] == 'voucher_summary':
                    # Build the voucher summary items
                    voucher_summary = line_splt[1].split(',')
                    voucher_summary_item = {
                        'description': voucher_summary[0],
                        'quantity': int(voucher_summary[1]),
                        'total_cost': float(voucher_summary[2])
                        }
                    voucher_summaries[voucher_summary[0]] = voucher_summary_item
                    voucher_values+=voucher_summary_item['quantity']
                elif line_splt[0] == 'voucher_fields':
                    are_vouchers = True
                    headers['voucher_fields'] = line_splt[1].split(',')
                else:
                    headers[line_splt[0]] = line_splt[1]
            line = input_file.readline().rstrip('\r\n')
        if input_file:
            input_file.close()
        self.validate(vouchers, voucher_values, file_input_path)
        


if __name__ == '__main__':
    try:
        file_input_path = input("Please enter file path: ")
    except: raise Exception('Invalid Path Entered')

    headers = {}
    vouchers = [] 
    line_items = []
    voucher_summaries = {}  
    voucher_averages = {}  
    voucher_print = VoucherPrinter()
    voucher_print.main(file_input_path)
