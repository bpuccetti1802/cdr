package it.sistinf.romacapitale.management.repository;

import it.sistinf.romacapitale.core.persistence.sql.AbstractRepository;
import it.sistinf.romacapitale.management.entity.NodoStrutturaEntity;
import org.springframework.stereotype.Repository;

@Repository
public class NodoStrutturaRepository extends AbstractRepository<Long, NodoStrutturaEntity> {

    public NodoStrutturaRepository() {
        super(NodoStrutturaEntity.class);
    }
}
