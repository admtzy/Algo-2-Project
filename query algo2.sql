create table sayur(id_sayur serial primary key, nama_sayur varchar(30) not null, stok integer not null, harga_satuan integer not null)

create table akun (id_akun serial primary key, nama varchar (30) not null,no_hp varchar(12) not null, password varchar(8) not null, status_akun varchar(1) not null)

create table lokasi (id_lokasi serial primary key,latitude numeric not null, longitude numeric not null, id_akun integer references akun(id_akun))

create table request_pembelian(id_request serial primary key,id_akun integer references akun(id_akun), id_sayur integer references sayur(id_sayur), nama_sayur varchar (30) not null, jumlah_beli integer not null, total_harga integer not null, status varchar (1) not null)

create table transaksi (id_transaksi serial primary key, id_request integer references request_pembelian(id_request),tanggal date not null)