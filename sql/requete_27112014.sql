SELECT * FROM quartier

--Liste des lampadaires d'un état X d'un quartier Y
create or replace function etat_quartier(etat text, quartier integer)
  returns table (param_id integer, param_states text, param_geom geometry)
as
$body$
	SELECT l.gid,l.states,l.geom
	FROM quartier AS q
	JOIN lampadaire AS l
	ON st_dwithin(l.geom,q.geom,0)
	WHERE l.states = $1 
	AND q.gid = $2
$body$
language sql;

-- Test : SELECT * FROM etat_quartier('ok',2)

